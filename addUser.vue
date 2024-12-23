<style>
	.addUser_tableTitle {
		border: 1px solid;
		flex: 1;
		text-align: center;
		border-left: 0;
		border-top: 0;
	}

	.addUser_addBut {
		width: 80px;
		height: 36px;
		text-align: center;
		margin: 10px 0;
		line-height: 36px;
	}
	@import url("./turnPageBar.css");
</style>
<template>
	<frame v-model="s_addInput" :s_display="s_display" :s_title="s_title" :f_submit="o_add.f_submit"
		:f_cancel="o_add.f_cancel" :f_close="o_add.f_close">
		<select v-model="s_gender" style="width:80px;border: 1px solid black;height: 36px;text-indent: 12px;">
			<option style="line-height:30px;">男</option>
			<option>女</option>
		</select>
	</frame>
	<div class="" style="width: 80%; margin: auto;">
		<div @click="o_add.f_add" class="addUser_addBut bg-blue-500  text-white font-bold  rounded">
			添加
		</div>
		<div style="border-top:1px solid;border-left:1px solid;">
			
			<!--head-->
			<div style="display: flex;">
				<div v-for="o_a in o_add.a_listHead" class="addUser_tableTitle">
					{{o_a.s_name}}
				</div>
			</div>
			<!--content-->
			<div>
				<div v-for="o_a in a_listContent" style="display: flex;line-height: 56px;">
					<div class="addUser_tableTitle">{{o_a.uid}}</div>
					<div class="addUser_tableTitle">{{o_a.name}}</div>
					<div class="addUser_tableTitle">{{o_a.gender}}</div>
					<div class="addUser_tableTitle">
						<button class="addUser_addBut bg-blue-500  text-white font-bold  rounded" @click="o_add.f_edit(o_a)">编辑</button>
					</div>
				</div>
			</div>
		</div>
	</div>
	<div id="js_barBox" style="margin-top: 10px;"></div>
</template>

<script setup>
	import frame from "../components/frame.vue";
	import root from "../assets/js/root.js";
	import F_turnPageBar from "../assets/js/turnPageBar/turnPageBar.js"
	import {
		ref,
		onMounted
	} from "vue";
	const s_display = ref("none");
	const s_addInput = ref("");
	const s_gender = ref("");
	const s_title =  ref("添加用户");
	const a_listContent = ref([]);
	const o_add = {
		a_listHead: [{
				s_name: "id",
			},
			{
				s_name: "名称",
			},
			{
				s_name: "性别",
			},
			{
				s_name: "编辑",
			}
		],
		f_submit: function() {
			o_main.f_submit();
		},
		f_cancel: function() {
			o_main.f_hidFrame(s_display);

		},
		f_close: function() {
			o_main.f_hidFrame(s_display);
		},

		f_add: function() {
			o_main.f_addFrameInit();
			o_main.f_setButState("add");
			o_main.f_showFrame(s_display);

		},
		f_edit: function(co){
			o_main.f_EditFrameInit(co);
			o_main.f_setButState("edit");
			o_main.f_showFrame(s_display);
		}
	}; 
	const o_main = Object.create(root);
	o_main.f_main = function(){
		onMounted(()=>{
			this.f_init();
			this.f_renderListC();
		})
	}
	o_main.f_init = function(){
		this.s_butType = "";//add edit
		this.n_userEditId = 0;
		this.n_currentPage = 1;//当前页面数
	}
	o_main.f_setButState = function(cs_type){
		this.s_butType = cs_type;
	}
	o_main.f_showFrame = function(co) {
		co.value = "block";
	}
	o_main.f_hidFrame = function(co) {
		co.value = "none";
	}
	o_main.f_addUser = async function(co) {
		const s_url = `api/add?name=${s_addInput.value}&gender=${s_gender.value}`;
		const respone = await this.o_request.f_fetchC(s_url);
		return respone;
	}
	o_main.f_edit = async function(co_data) {
		const s_url = `api/edit?uid=${this.n_userEditId}&name=${s_addInput.value}&gender=${s_gender.value}`;
		const respone = await this.o_request.f_fetchC(s_url);
		return respone;
	}
	o_main.f_getList = async function(co) {
		const s_url = `api/getList?n_currentPage=${this.n_currentPage}`;
		const response = await this.o_request.f_fetchC(s_url);
		return response;
	}
	o_main.f_renderListC = async function(){//获取 列表数据 集合
		const response = await this.f_getList();
		if(response){
			a_listContent.value = response;
			this.f_creTurnPageBar(response[0].total);
		}
	}
	o_main.f_submit = async function(co){
		if(this.s_butType === "add"){
			const response = await this.f_addUser();
			if(response && response.state){
				this.f_renderListC();
			}else{
				alert("添加用户失败")
			}
		}else if(this.s_butType === "edit"){
			const response = await this.f_edit(co);
			if(response && response.state){
				this.f_renderListC();
			}else{
				alert("修改失败")
			}
		}
		this.f_hidFrame(s_display);
	}
	o_main.f_addFrameInit = async function(){
		s_title.value = "添加用户";
		s_addInput.value = "";//名称输入框
		s_gender.value = "男"
	}
	o_main.f_EditFrameInit = async function(co){
		this.n_userEditId = co.uid;//用户的id
		s_title.value = "编辑";
		s_addInput.value = co.name;//名称输入框
		s_gender.value = co.gender;
	}
	o_main.f_creTurnPageBar = function(cn_turnLen){//创建翻页条
		var o_turnPageBar = new F_turnPageBar({
			e_parent:document.getElementById("js_barBox"),
			n_turnLen:Math.ceil(cn_turnLen / 7),//页面总数
			//n_currentPage:9,//当前页面数
			n_butLen:cn_turnLen,//翻页条的长度(此值不能小于7)
			f_selectData:(n_a)=>{//数据被选中时执行
			   this.n_currentPage = n_a;
				this.f_renderListC();
				console.log(n_a)
			}
		});
		o_turnPageBar.f_main();
	}
	o_main.f_main();
</script>
